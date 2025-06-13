package com.ruoyi.entertainment.controller;

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
import com.ruoyi.entertainment.domain.Entertainment;
import com.ruoyi.entertainment.service.IEntertainmentService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 娱乐信息Controller
 * 
 * @author ningf
 * @date 2024-07-09
 */
@RestController
@RequestMapping("/entertainment")
public class EntertainmentController extends BaseController
{
    @Autowired
    private IEntertainmentService entertainmentService;

    /**
     * 查询娱乐信息列表
     */
    @RequiresPermissions("entertainment:entertainment:list")
    @GetMapping("/list")
    public TableDataInfo list(Entertainment entertainment)
    {
        startPage();
        List<Entertainment> list = entertainmentService.selectEntertainmentList(entertainment);
        return getDataTable(list);
    }

    /**
     * 导出娱乐信息列表
     */
    @RequiresPermissions("entertainment:entertainment:export")
    @Log(title = "娱乐信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Entertainment entertainment)
    {
        List<Entertainment> list = entertainmentService.selectEntertainmentList(entertainment);
        ExcelUtil<Entertainment> util = new ExcelUtil<Entertainment>(Entertainment.class);
        util.exportExcel(response, list, "娱乐信息数据");
    }

    /**
     * 获取娱乐信息详细信息
     */
    @RequiresPermissions("entertainment:entertainment:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(entertainmentService.selectEntertainmentById(id));
    }

    /**
     * 新增娱乐信息
     */
    @RequiresPermissions("entertainment:entertainment:add")
    @Log(title = "娱乐信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Entertainment entertainment)
    {
        return toAjax(entertainmentService.insertEntertainment(entertainment));
    }

    /**
     * 修改娱乐信息
     */
    @RequiresPermissions("entertainment:entertainment:edit")
    @Log(title = "娱乐信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Entertainment entertainment)
    {
        return toAjax(entertainmentService.updateEntertainment(entertainment));
    }

    /**
     * 删除娱乐信息
     */
    @RequiresPermissions("entertainment:entertainment:remove")
    @Log(title = "娱乐信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(entertainmentService.deleteEntertainmentByIds(ids));
    }
}
