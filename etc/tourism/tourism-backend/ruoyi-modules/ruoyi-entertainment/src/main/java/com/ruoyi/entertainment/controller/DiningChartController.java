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
import com.ruoyi.entertainment.domain.Dining;
import com.ruoyi.entertainment.service.IDiningService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 餐饮信息Controller
 *
 * @author ningf
 * @date 2024-07-09
 */
@RestController
@RequestMapping("/diningChart")
public class DiningChartController extends BaseController
{
    @Autowired
    private IDiningService diningService;

    /**
     * 查询餐饮信息列表
     */
    @RequiresPermissions("entertainment:diningChart:list")
    @GetMapping("/list")
    public TableDataInfo list(Dining dining)
    {
        startPage();
        List<Dining> list = diningService.selectDiningList(dining);
        return getDataTable(list);
    }

    /**
     * 导出餐饮信息列表
     */
    @RequiresPermissions("entertainment:diningChart:export")
    @Log(title = "餐饮信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Dining dining)
    {
        List<Dining> list = diningService.selectDiningList(dining);
        ExcelUtil<Dining> util = new ExcelUtil<Dining>(Dining.class);
        util.exportExcel(response, list, "餐饮信息数据");
    }

    /**
     * 获取餐饮信息详细信息
     */
    @RequiresPermissions("entertainment:diningChart:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(diningService.selectDiningById(id));
    }

    /**
     * 新增餐饮信息
     */
    @RequiresPermissions("entertainment:diningChart:add")
    @Log(title = "餐饮信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Dining dining)
    {
        return toAjax(diningService.insertDining(dining));
    }

    /**
     * 修改餐饮信息
     */
    @RequiresPermissions("entertainment:diningChart:edit")
    @Log(title = "餐饮信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Dining dining)
    {
        return toAjax(diningService.updateDining(dining));
    }

    /**
     * 删除餐饮信息
     */
    @RequiresPermissions("entertainment:diningChart:remove")
    @Log(title = "餐饮信息", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(diningService.deleteDiningByIds(ids));
    }
}
