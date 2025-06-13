package com.ruoyi.emergency.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.emergency.domain.Emergencyinfo;
import com.ruoyi.emergency.service.IEmergencyinfoService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 应急信息Controller
 * 
 * @author ningf
 * @date 2024-07-12
 */
@RestController
@RequestMapping("/emergencyinfo")
public class EmergencyinfoController extends BaseController
{
    @Autowired
    private IEmergencyinfoService emergencyinfoService;

    /**
     * 查询应急信息列表
     */
    @GetMapping("/list")
    public TableDataInfo list(Emergencyinfo emergencyinfo)
    {
        startPage();
        List<Emergencyinfo> list = emergencyinfoService.selectEmergencyinfoList(emergencyinfo);
        return getDataTable(list);
    }

    /**
     * 导出应急信息列表
     */
    @RequiresPermissions("emergency:emergencyinfo:export")
    @Log(title = "应急信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Emergencyinfo emergencyinfo)
    {
        List<Emergencyinfo> list = emergencyinfoService.selectEmergencyinfoList(emergencyinfo);
        ExcelUtil<Emergencyinfo> util = new ExcelUtil<Emergencyinfo>(Emergencyinfo.class);
        util.exportExcel(response, list, "应急信息数据");
    }

    /**
     * 获取应急信息详细信息
     */
    @RequiresPermissions("emergency:emergencyinfo:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(emergencyinfoService.selectEmergencyinfoById(id));
    }

    /**
     * 新增应急信息
     */
    @RequiresPermissions("emergency:emergencyinfo:add")
    @Log(title = "应急信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Emergencyinfo emergencyinfo)
    {
        return toAjax(emergencyinfoService.insertEmergencyinfo(emergencyinfo));
    }

    /**
     * 修改应急信息
     */
    @RequiresPermissions("emergency:emergencyinfo:edit")
    @Log(title = "应急信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Emergencyinfo emergencyinfo)
    {
        return toAjax(emergencyinfoService.updateEmergencyinfo(emergencyinfo));
    }

    /**
     * 删除应急信息
     */
    @RequiresPermissions("emergency:emergencyinfo:remove")
    @Log(title = "应急信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(emergencyinfoService.deleteEmergencyinfoByIds(ids));
    }

    @RequiresPermissions("emergency:emergencyinfo:confirm")
    @DeleteMapping("/confirm/{ids}")
    public AjaxResult confirm(@PathVariable Long[] ids)
    {
        return toAjax(emergencyinfoService.confirmEmergencyinfoByIds(ids));
    }
}
